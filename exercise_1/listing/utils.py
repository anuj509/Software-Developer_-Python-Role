from django.http import HttpResponse
import json
import re


class StandardResponse():
  """
  Class to provide standard response
  """
  def Response(status,message,data=None):
    try:
      respDict = {"status": status, "message": message, "data":data}
      
      if data==None:
        respDict = {"status": status, "message": message}
      return HttpResponse(json.dumps(respDict), content_type='application/json')
    except Exception as e:
      respDict = {"status": False, "message": str(e)}
      return HttpResponse(json.dumps(respDict), content_type='application/json')

class InputDetails():
    """
    Class to create input data details object
    """
    def __init__(self, required=True, canBeEmpty=False, inType=None, inPattern=None, minLength=None, maxLength=None,minVal=None, maxVal=None, exactMatch=[],charSet=[],endWith=[]):
        varTypes = {
            'int': int,
            'float': float,
            'str': str,
            'string':str,
            'dict':dict,
            None:None
        }

        self.required = required        #default is True
        self.canBeEmpty = canBeEmpty    #default is False     
        self.inType = inType
        self.varType = varTypes[inType] #converting from 'str' to 'type'
        self.minLength = minLength      #for string input 
        self.maxLength = maxLength
        self.minVal = minVal            #for int input
        self.maxVal = maxVal
        self.inPattern = inPattern
        self.exactMatch = exactMatch
        self.charSet = charSet          # 'a-z','A-Z', '0-9', ' ', '/',':', etc.
        self.endWith = endWith


class InputValidation():
    """
    Class to validate input data and give appropriate response
    """
    def Response(inputParams,paramDetails):

        isParmasValid = True 
        message = "Valid input"
        try:
            for key,val in paramDetails.items():

                #check if required parameter is missing
                if val.required and not key in inputParams.keys():
                    isParmasValid = False
                    message = "Parameter "+key+" is missing."
                    break
                elif val.required==False and not key in inputParams.keys():
                    continue
                
                #check if parameter is empty
                if not val.canBeEmpty and not inputParams[key]:
                    isParmasValid = False
                    message = "Parameter "+key+" can not be empty."
                    break
                elif val.canBeEmpty and not inputParams[key]:
                  continue
                
                #check if input type is correct
                if val.inType and not isinstance(inputParams[key], val.varType):
                    isParmasValid = False
                    message = "Parameter "+key+" should be "+ val.inType+"."
                    break

                if isinstance(inputParams[key], str): 
                    #check minimum length (for string input)
                    if val.minLength and not len(inputParams[key])>=val.minLength:
                        isParmasValid = False
                        message = "Minimum length of "+key+" should be "+ str(val.minLength)+"."
                        break

                    #check maximum length (for string input)
                    if val.maxLength and not len(inputParams[key])<=val.maxLength:
                        isParmasValid = False
                        message = "Maximum length of "+key+" should be "+ str(val.maxLength)+"."
                        break

                if isinstance(inputParams[key], int): 
                    #check minimum value (for int input)
                    if val.minVal and not inputParams[key] >= val.minVal:
                        isParmasValid = False
                        message = "Minimum value of "+key+" should be "+ str(val.minVal)+"."
                        break

                    #check maximum value (for int input)
                    if val.maxVal and not inputParams[key] <= val.maxVal:
                        isParmasValid = False
                        message = "Maximum value of "+key+" should be "+ str(val.maxVal)+"."
                        break

                #check if string is exact match
                if val.exactMatch and not inputParams[key] in val.exactMatch:
                    isParmasValid = False
                    message = key+" should be one of following - "+', '.join(str(x) for x in val.exactMatch)+"."
                    break
                
                #Validation for lowercase, uppercase, spaces, special characters
                if val.charSet:

                    #check if characters are in lowercase 
                    if not 'a-z' in val.charSet and any(c.islower() for c in inputParams[key]):                    
                        isParmasValid = False
                        message = key+" should not contain lowercase letters."
                        break
                    
                    #check if characters are in uppercase
                    if not 'A-Z' in val.charSet and any(c.isupper() for c in inputParams[key]):                    
                        isParmasValid = False
                        message = key+" should not contain uppercase letters."
                        break

                    #check if there are any digits
                    if not '0-9' in val.charSet and any(c.isdigit() for c in inputParams[key]):                    
                        isParmasValid = False
                        message = key+" should not contain any digits."
                        break

                    #check if there are any spaces
                    if not " " in val.charSet and any(c.isspace() for c in inputParams[key]):
                        isParmasValid = False
                        message = key+" should not contain spaces."
                        break

                    #check if there are any special chars
                    if any(not c.isalnum() for c in inputParams[key]):
                        
                        specialChars = set([c for c in inputParams[key] if not c.isalnum()])
                        charsAllowed = set(val.charSet) - set(['a-z','A-Z','0-9',' '])
                        charsNotAllowed = specialChars - charsAllowed - set([' '])

                        if not (len(charsNotAllowed) == 0):
                            isParmasValid = False
                            message = key+" should not contain special characters."
                            if not len(charsAllowed) ==0:
                                message +="(Except '"+"', '".join(str(x) for x in charsAllowed)+"')"
                            break

                #check if string ends with particular string
                if val.endWith and not inputParams[key].endswith(tuple(val.endWith)):
                    isParmasValid = False
                    message = key+" should end with "+', '.join(str(x) for x in val.endWith)
                    break

                #check if string matches given pattern
                if val.inPattern:
                    pat = re.compile(val.inPattern)
                    if not re.fullmatch(pat, inputParams[key]):
                        isParmasValid = False
                        message = key+" does not match with given pattern."
                        break
                    
            return (isParmasValid,message)

        except Exception as e:
            return (False,str(e))      