from flask import (jsonify, make_response, Response)
from werkzeug.exceptions import HTTPException


def app_error(msg: str, status_code: int, error: str = 'Error') -> Response:
  """
  Creates a custom error response which can be thrown from anywhere
  inside the app
  """
  response = jsonify({
      'status': error,
      'message': msg,
      'data': None,
      'code': status_code
  })
  response = make_response(response)
  return response, status_code



def catch_error():
  """
  Catches all app errors
  """
  def decorate(f):
    def applicator(*args, **kwargs):
      try:
         return f(*args,**kwargs)
      except Exception as e:
        return error_response(e)
    return applicator
  return decorate


def error_response(e: Exception) -> Response:
  """
  Creates error response. 
  If exception is of type HTTPException it returns a known http exception
  Else it returns a generic 500 internal server error
  """
  if isinstance(e, HTTPException):
      return app_error(e.description, e.code, 'error')

  e = {'name': 'Internal server error', 'description': 'Something went wrong', 'code': 500}
  return app_error(e['description'], e['code'], 'error')

