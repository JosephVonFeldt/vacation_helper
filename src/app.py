from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def main():
    return '''
     <form action="/echo_user_input" method="POST">
         <select name="city" id="city-select">
          <option value="">--Please choose an option--</option>
          <option value="Boulder">Boulder</option>
          <option value="Denver">Denver</option>
          <option value="New York">New York</option>
         </select>
         <input name="user_input">
         <input type="submit" value="Submit!">
     </form>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    city = request.form.get("city", "")
    input_text = request.form.get("user_input", "")
    return "You entered: " + input_text + " "+ city