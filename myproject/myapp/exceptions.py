from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

def custom_exception_handler(exc, context):
  
    
  
    response = exception_handler(exc, context)

   
    if response is not None:
        return response

 
    if isinstance(exc, ValueError):
      
        logger.error(f"ValueError Caught: {exc} in view {context['view'].__class__.__name__}")
        
       
        return Response(
            {'error': str(exc), 'status': 'Bad Request', 'code': 'VALUE_ERROR'},
            status=status.HTTP_400_BAD_REQUEST
        )

   
    logger.exception(f"CRITICAL ERROR: Unhandled exception: {exc}")
    
    
    return Response(
        {'error': 'Internal Server Error', 'status': 'Server Error', 'code': 'UNHANDLED_ERROR'},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )