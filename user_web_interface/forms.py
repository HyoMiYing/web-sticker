from django import forms

class GameForm(forms.Form):

    def __init__(self, card_list, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)

        for row, cards in enumerate(card_list):
            for card in range(cards):
                self.fields[f'row{row}card{card}'] = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'checkbox'}),required=False, label=' ')
                self.label_suffix = ''
                # self.fields[f'row{row}card{card}'].label = '<label>yy</label>'

    def clean(self):
        checkboxes = super(GameForm, self).clean()

        if not any(
            checkboxes.get(x, False)
            for x in (
                self.fields
            )
        ):
            first_checkbox = list(self.fields.keys())[0]
            self._errors[first_checkbox] = self.error_class([('You must select at least one card.')])

        return checkboxes

    def as_div(self):
        return self._html_output(
            normal_row = u'<div class="custom-checkbox-input" %(html_class_attr)s>%(errors)s%(field)s %(label)s%(help_text)s</div>',
            error_row = u'<div>%s</div>',
            row_ender = '</div>',
            help_text_html = u' <span class="helptext">%s</span>',
            errors_on_separate_row = False,
        )