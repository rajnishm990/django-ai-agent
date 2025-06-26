from langchain_core.tools import tool  #tool decorator makes python funcs into langchain tools
from langchain_core.runnables import RunnableConfig #config allows us to pass something like user_id . We can't directly make user_id a argument of function due to security concern 
from documents.models import Document
from django.db.models import Q


@tool
def list_documents(limit: int = 5, config:RunnableConfig ={}):
    ''' list 5 most recent LIMIT documents for the current user with maximum of 25 
    
    limit: int , number of documents (max=25)
    '''
    if limit> 25:
        limit= 25
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
def search_query_documents(query: str, limit: int= 5 , config:RunnableConfig = {}):
    """
    search the most recent LIMIT document based on a limit for a user with max limit of 25

    query : str for the lookup searche for title or content of documents
    limit : int represening number of results (max=25)
    
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get(user_id)
    default_lookups={
        'owner_id' :user_id,
        'active': True
    }
    qs = Document.objects.filter(**default_lookups).filter(Q(title__icontains=query) | Q(content__incontains=query)).order_by('-created_at')
    respone_data = []
    for obj in qs[0:limit]:
        respone_data.append({'id':obj.id , 'title': obj.title , 'content': obj.content})
    return respone_data



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

@tool
def update_document(document_id: int,title: str= None, content: str = None, config: RunnableConfig={}):
    """ updates a document for a user by document id 
    
    document_id : int representing ID of document(required)
    title : str (optional)
    content: long form text (optional)
    
    """
    configurable = config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception('Invalid request for this user')
    try:
        obj = Document.objects.get(owner_id = user_id , document_id=document_id)
    except Document.DoesNotExist:
        raise Exception("Document doesnt exist  , Try again")
    except :
        raise Exception("Invalid request for a document , please try again")
    if title is not None:
        obj.title = title
    if content is not None:
        obj.content = content
    if title or content:
        obj.save()
    response_data = {
        'id': obj.id,
        "title": obj.title,
        'content': obj.content,
        'updated_at': obj.updated_at
    }
    return response_data


@tool
def delete_document(document_id: int , config: RunnableConfig):
    """ 
    Deletes a document for a user by its given document Id 
    
    document_id: Int representing Id of the document (required)

    """
    configurable= config.get('configurable') or config.get('metadata')
    user_id = configurable.get('user_id')
    if user_id is None:
        raise Exception("request invalid for given user")
    try:
        obj = Document.objects.get(owner_id=user_id , document_id=document_id)
    except Document.DoesNotExist:
        raise Exception("Document doesn't exists, try again ")
    except :
        raise Exception("Invalid request for this document , please try again")
    obj.delete()
    response_data = {
        'message':'success'
    }
    return response_data
    


document_tools = [list_documents, get_document, create_document, delete_document, update_document]


