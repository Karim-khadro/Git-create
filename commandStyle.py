from PyInquirer import style_from_dict, Token

# * Printing style for the questions
style = style_from_dict({
    Token.Separator: '#00FF00',
    Token.QuestionMark: '#E91E63 bold',
    Token.Selected: '#673AB7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#2196f3 bold',
    Token.Question: '',

})


