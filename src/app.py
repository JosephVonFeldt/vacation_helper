from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def main():
    return '''
     <form action="/echo_user_input" method="POST">
         <select name="city" id="city-select">
          <option value="">--Please choose a Departure City--</option>
          <option value="Los Angeles">Los Angeles</option>
          <option value="Madison">Madison</option>
          <option value="New York">New York</option>
         </select>
         <br>
         Vacation Type: <br>
         <input type="radio" id="Snow" name="vacation" value="Snow" checked >
            <label for="Snow">Snow</label><br>
            <input type="radio" id="Beach" name="vacation" value="Beach">
            <label for="Beach">Beach</label><br>
            <input type="radio" id="Hiking" name="vacation" value="Hiking">
            <label for="Hiking">Hiking</label>
         <br>
         <input name="user_input" placeholder="Text to Echo">
         <input type="submit" value="Submit">
     </form>
     '''

@app.route("/echo_user_input", methods=["POST"])
def echo_input():
    city = request.form.get("city", "")
    vacation_type = request.form.get("vacation", "")
    input_text = request.form.get("user_input", "")
    return f"User Input Echo: {input_text} <br> " \
           f"Start City: {city} <br> " \
           f"Suggested Destination City: {calcCity(vacation_type)} "

def calcCity(vacation_type):
    if vacation_type == "Snow":
        return "Denver"
    elif vacation_type == "Beach":
        return "San Diego"
    elif vacation_type == "Hiking":
        return "Salk Lake City"
    else:
        return "New York"
