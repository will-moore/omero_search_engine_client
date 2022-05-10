import os


def get_help_file_contenets():
    '''
     get the content of the help file, it will be displayed in the app help tab
    '''
    lines_=[]
    help_file = os.path.join(os.path.abspath(os.path.dirname(__file__)),
                                        'help.txt')
    if not os.path.isfile(help_file):
         return (lines_)
    with open(help_file) as help:
        lines_ = help.readlines()
    lines=[x.replace("\n","") for x in lines_ ]
    return (lines)