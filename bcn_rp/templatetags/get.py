from django.template import Library
import sys

register = Library()

@register.filter
def get( dict, key, default = '' ):
  """
  Usage:

  view:
  some_dict = {'keyA':'valueA','keyB':{'subKeyA':'subValueA','subKeyB':'subKeyB'},'keyC':'valueC'}
  keys = ['keyA','keyC']
  template:
  {{ some_dict|get:"keyA" }}
  {{ some_dict|get:"keyB"|get:"subKeyA" }}
  {% for key in keys %}{{ some_dict|get:key }}{% endfor %}
  """

  try:

      print("dictionary: " + str(dict))
      sys.stdout.flush()

      return dict.get(key,default)
  except:
      return default