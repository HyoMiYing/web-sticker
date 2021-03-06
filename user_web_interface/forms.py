from django import forms

class CreateNewGameForm(forms.Form):
    NUMBER_OF_ROUNDS_CHOICES = [(x+3, f'{x+3} rounds') for x in range(9)]

    player1 = forms.CharField(min_length=3, max_length=20, empty_value='player1', label='Player 1\'s name', label_suffix=": ")
    player2 = forms.CharField(min_length=3, max_length=20, empty_value='player2', label='Player 2\'s name', label_suffix=": ")
    number_of_rounds = forms.ChoiceField(choices=NUMBER_OF_ROUNDS_CHOICES, initial=(7, '7 rounds'), label='Number of rounds', label_suffix=": ")

class CreateNewGameVsMachineForm(forms.Form):
    NUMBER_OF_ROUNDS_CHOICES = [(x+3, f'{x+3} rounds') for x in range(9)]

    your_name = forms.CharField(min_length=3, max_length=20, empty_value='cho-cho-lino', label='Your name', label_suffix=": ")
    number_of_rounds = forms.ChoiceField(choices=NUMBER_OF_ROUNDS_CHOICES, initial=(7, '7 rounds'), label='Number of rounds', label_suffix=": ")

class GameForm(forms.Form):

    def __init__(self, card_list, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)

        for row, cards in enumerate(card_list):
            for card in range(cards):
                self.fields[f'row{row}card{card}'] = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'checkbox'}),required=False, label=' ')
                self.label_suffix = ''

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
