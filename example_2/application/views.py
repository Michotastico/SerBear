from serbear import View
from utilities.responses import html_response


class HomeView(View):

    def get(self, request):
        rendered_template = self.render_template(
            'index.html',
            {
                'framework': 'Ser-Bear',
                'framework_pun': 'Its bear-ly functional'
            }
        )
        return html_response(rendered_template)
