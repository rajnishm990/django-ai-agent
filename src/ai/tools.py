from documents.models import Document

def list_documents():
    ''' get all the documents for the current user  '''
    qs = Document.objects.filter(active=True)
    response_data = []
    for obj in qs:
        response_data.append({
            'id': obj.id,
            'title': obj.title
        })
    return response_data

def get_document(document_id: int):
    ''' get a details of document for the current user '''
    qs = Document.objects.get(id=document_id, active=True)
    response_data = {
        'id': qs.id ,
        'title': qs.title,
        'content': qs.content
    }
    return response_data

