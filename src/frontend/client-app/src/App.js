import logo from './logo.svg';
import './App.css';
import './components/SelectDepartureCity'
import DepartureList from "./components/SelectDepartureCity";
import VacationTypes from "./components/SelectVacationType";
import React, { createContext, useState, useEffect} from "react";
import axios from 'axios'
import SuggestedDestination from "./components/SuggestedDestination";

export const airportContext = createContext();
export const vacationContext = createContext();

export const suggestionsContext = createContext();

function onClick(selectedAirport, selectedVacation, setSuggestion) {
    axios.get(`http://127.0.0.1:5000/VF/${selectedAirport}/${selectedVacation}`).then(response => {
            console.log("SUCCESS", response)
            setSuggestion(response.data)
            }).catch(error => {
            console.log(error)
            })
}
function App() {

    const [selectedAirport, setSelectedAirport] = useState('DEN');
    const [selectedVacation, setSelectedVacation] = useState('Snow');
    const [suggestion, setSuggestion] = useState('');
    let [cities, setCities] = useState([{'CITY': 'DENVER', "AP": "DEN", "KEY": 0}])
    useEffect(() => {
        if (cities.length < 2){
            axios.get('http://127.0.0.1:5000/cities').then(response => {
            console.log("SUCCESS", response)
            setCities(response.data)
            }).catch(error => {
            console.log(error)
            })
        }

    });
    return (
        <div className="App">
            <header className="App-header">
                <img src={logo} className="App-logo" alt="logo"/>
                <p>
                    Edit <code>src/App.js</code> and save to reload.
                </p>
                <a
                    className="App-link"
                    href="https://reactjs.org"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    TEST
                </a>
                <airportContext.Provider value={{selectedAirport, setSelectedAirport}}>
                    <DepartureList cities={cities}/>
                </airportContext.Provider>
                <vacationContext.Provider value = {{selectedVacation, setSelectedVacation}}>
                    <VacationTypes/>
                </vacationContext.Provider>

                <button onClick={() => {
                    onClick(selectedAirport, selectedVacation, setSuggestion)
                }}>
                    Find Vacations
                </button>
                <suggestionsContext.Provider value = {{suggestion, setSuggestion}}>
                    {suggestion? <SuggestedDestination/>: null}
                </suggestionsContext.Provider>

            </header>

        </div>
    );
}

export default App;
