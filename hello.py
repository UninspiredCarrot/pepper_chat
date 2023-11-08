file = open("pepper.html", "w")

message = '''

<html>

<head></head>

<body>
<h4>Hi I'm Pepper. Can I assist you today</h4>

<button> Yes </button>

<button> No </button>

</body>

</html>
'''

file.write(message)
file.close()
