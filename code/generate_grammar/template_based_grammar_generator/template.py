class Template():
    """
    params is a dictionary, because every template can have different parameters
    and this way it's easier to pass them to format() by kwarg 
    """
    def __init__(self):
        self.name = ""
        self.params = {}
        self.rtg_type = ""


    def render(self):
        with open("templates/{}.tpl".format(self.name), "r") as tpl_file:
            template = tpl_file.read()
            result = self.rtg_type + "\n"
            result += template.format(**self.params)
        return result

