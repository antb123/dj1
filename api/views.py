from django.http import JsonResponse, FileResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.conf import settings
from django.core.exceptions import ValidationError
import json
from folders.models import Folder
from documents.models import Document


@login_required
@require_http_methods(["GET", "POST"])
def folder_list(request):
    """List folders or create a new folder."""

    if request.method == "GET":
        folders = Folder.objects.filter(owner=request.user)
        data = {
            'folders': [
                {
                    'id': folder.id,
                    'name': folder.name,
                    'parent_id': folder.parent.id if folder.parent else None,
                    'file_count': folder.get_file_count(),
                    'created_at': folder.created_at.isoformat(),
                }
                for folder in folders
            ]
        }
        return JsonResponse(data)

    elif request.method == "POST":
        try:
            data = json.loads(request.body)
            name = data.get('name', '').strip()
            parent_id = data.get('parent_id')

            if not name:
                return JsonResponse({'success': False, 'error': 'Folder name is required'}, status=400)

            parent = None
            if parent_id:
                try:
                    parent = Folder.objects.get(id=parent_id, owner=request.user)
                except Folder.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Parent folder not found'}, status=404)

            folder = Folder.objects.create(
                name=name,
                owner=request.user,
                parent=parent
            )

            return JsonResponse({
                'success': True,
                'folder': {
                    'id': folder.id,
                    'name': folder.name,
                    'parent_id': folder.parent.id if folder.parent else None,
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET", "PUT", "DELETE"])
def folder_detail(request, folder_id):
    """Get, update, or delete a specific folder."""

    try:
        folder = Folder.objects.get(id=folder_id, owner=request.user)
    except Folder.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Folder not found'}, status=404)

    if request.method == "GET":
        return JsonResponse({
            'id': folder.id,
            'name': folder.name,
            'parent_id': folder.parent.id if folder.parent else None,
            'file_count': folder.get_file_count(),
            'total_size': folder.get_total_size(),
        })

    elif request.method == "PUT":
        try:
            data = json.loads(request.body)
            if 'name' in data:
                folder.name = data['name'].strip()
            if 'parent_id' in data:
                if data['parent_id']:
                    parent = Folder.objects.get(id=data['parent_id'], owner=request.user)
                    folder.parent = parent
                else:
                    folder.parent = None
            folder.save()
            return JsonResponse({'success': True})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    elif request.method == "DELETE":
        folder.delete()
        return JsonResponse({'success': True})


@login_required
@require_http_methods(["GET", "POST"])
def document_list(request):
    """List documents or upload new documents."""

    if request.method == "GET":
        folder_id = request.GET.get('folder_id')

        if folder_id and folder_id != 'root':
            documents = Document.objects.filter(owner=request.user, folder_id=folder_id)
        elif folder_id == 'root':
            documents = Document.objects.filter(owner=request.user, folder=None)
        else:
            documents = Document.objects.filter(owner=request.user)

        data = {
            'documents': [
                {
                    'id': doc.id,
                    'name': doc.name,
                    'file_type': doc.file_type,
                    'file_size': doc.file_size,
                    'readable_size': doc.get_readable_size(),
                    'folder_id': doc.folder.id if doc.folder else None,
                    'uploaded_at': doc.uploaded_at.isoformat(),
                }
                for doc in documents
            ]
        }
        return JsonResponse(data)

    elif request.method == "POST":
        try:
            files = request.FILES.getlist('files')
            folder_id = request.POST.get('folder_id')

            if not files:
                return JsonResponse({'success': False, 'error': 'No files provided'}, status=400)

            folder = None
            if folder_id:
                try:
                    folder = Folder.objects.get(id=folder_id, owner=request.user)
                except Folder.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Folder not found'}, status=404)

            uploaded_docs = []
            for file in files:
                # Check file size
                if file.size > settings.MAX_UPLOAD_SIZE:
                    continue

                # Check storage quota
                if not request.user.has_storage_available(file.size):
                    return JsonResponse({
                        'success': False,
                        'error': 'Storage quota exceeded'
                    }, status=400)

                # Create document
                doc = Document(
                    name=file.name,
                    file=file,
                    owner=request.user,
                    folder=folder,
                    file_size=file.size
                )
                doc.save()
                uploaded_docs.append(doc.id)

            return JsonResponse({
                'success': True,
                'uploaded': len(uploaded_docs),
                'document_ids': uploaded_docs
            })

        except ValidationError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


@login_required
@require_http_methods(["GET", "DELETE"])
def document_detail(request, document_id):
    """Get or delete a specific document."""

    try:
        document = Document.objects.get(id=document_id, owner=request.user)
    except Document.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Document not found'}, status=404)

    if request.method == "GET":
        return JsonResponse({
            'id': document.id,
            'name': document.name,
            'file_type': document.file_type,
            'file_size': document.file_size,
            'readable_size': document.get_readable_size(),
            'folder_id': document.folder.id if document.folder else None,
            'uploaded_at': document.uploaded_at.isoformat(),
        })

    elif request.method == "DELETE":
        document.delete()
        return JsonResponse({'success': True})


@login_required
def document_download(request, document_id):
    """Download a document."""

    try:
        document = Document.objects.get(id=document_id, owner=request.user)
    except Document.DoesNotExist:
        raise Http404("Document not found")

    response = FileResponse(document.file.open('rb'), as_attachment=True, filename=document.name)
    return response
