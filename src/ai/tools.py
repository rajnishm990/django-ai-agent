from langchain_core.tools import tool  #tool decorator makes python funcs into langchain tools
from langchain_core.runnables import RunnableConfig #config allows us to pass something like user_id . We can't directly make user_id a argument of function due to security concern 
from documents.models import Document


@tool
def list_documents(config:RunnableConfig):
    ''' list 5 most recent documents for the current user  '''
    limit=5
    configurable = config.get('configurable') or config.get('metadata')   #both of these get us metadata , which we can then use to get user_id
    user_id = configurable.get('user_id')
    qs = Document.objects.filter(owner=user_id,active=True).order_by('-created_at')
    response_data = []
    for obj in qs[0:limit ]:
        response_data.append({
            'id': obj.id,
            'title': obj.title
        })
    return response_data

@tool
def get_document(document_id: int, config: RunnableConfig):
    ''' get a details of document for the current user '''
    
    configurable = config.get('configurable') or config.get('metadata') 
    user_id = configurable.get('user_id')
    try:
        obj = Document.objects.get(owner=user_id, id=document_id, active=True)
    except Document.DoesNotExist:
        raise Exception('Document Does not exist')
    except:
        raise Exception('Invalid request for this Document , try again')
    response_data = {
        'id': obj.id,
        'title': obj.title,
        'content': obj.content,
        'created_at': obj.created_at
    }
    return response_data

@tool
def create_document(title: str , content: str, config: RunnableConfig):
    """ 
    creates a new document to store for a user 
    
    Arguements:
    title: string max characters 120
    content : long form text in many paragraphs

    """
    confugurable = config.get('configurable') or config.get('metadata')
    user_id = confugurable.get('user_id')
    if user_id is None:
        raise Exception('Invalid request for user ')
    obj = Document.objects.create(title=title , content=content , owner_id = user_id)

    response_data = {
        'id': obj.id,
        'title': obj.title,
        'content': obj.content,
        'created_at': obj.created_at
    }
    return response_data

    


document_tools = [list_documents, get_document, create_document]


