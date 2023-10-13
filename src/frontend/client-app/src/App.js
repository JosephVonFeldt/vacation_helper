import logo from './logo.svg';
import './App.css';
import './components/SelectDepartureCity'
import DepartureList from "./components/SelectDepartureCity";
import VacationTypes from "./components/SelectVacationType";
import React, {createContext, useState, useEffect} from "react";
import axios from 'axios'
import SuggestedDestination from "./components/SuggestedDestination";
import {Button, createTheme, ThemeProvider} from "@mui/material";

export const airportContext = createContext();
export const vacationContext = createContext();

export const suggestionsContext = createContext();

function onClick(selectedAirport, selectedVacation, setSuggestion, setHasSuggestion) {
    axios.get(`${window.location.origin}/VF/${selectedAirport}/${selectedVacation}`).then(response => {
        //console.log("SUCCESS", response)
        setSuggestion(response.data)
        setHasSuggestion(true)
    }).catch(error => {
        console.log(error)
    })

}

function App() {
    const theme = createTheme({
        palette: {
            primary: {
                main: "#cfb87c",
            },
            secondary: {
                main: '#111111',
            },
        },
    });
    const [selectedAirport, setSelectedAirport] = useState('DEN');
    const [selectedVacation, setSelectedVacation] = useState('Beach');
    const [suggestion, setSuggestion] = useState('');
    const [hasSuggestion, setHasSuggestion] = useState(false);
    let [cities, setCities] = useState([{'CITY': 'DENVER', "AP": "DEN", "KEY": 0}])

    function ssv(str) {
        setSelectedVacation(str);
        setHasSuggestion(false)
    }

    function ssa(str) {
        setSelectedAirport(str);
        setHasSuggestion(false)
    }

    useEffect(() => {
        if (cities.length < 2) {
            axios.get(`${window.location.origin}/cities`).then(response => {
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
            </header>
            <ThemeProvider theme={theme}>
                <body>
                <airportContext.Provider value={{selectedAirport, ssa}}>
                    <DepartureList cities={cities}/>
                </airportContext.Provider>
                <vacationContext.Provider value={{selectedVacation, ssv}}>
                    <VacationTypes/>
                </vacationContext.Provider>


                <Button variant="contained" onClick={() => {
                    onClick(selectedAirport, selectedVacation, setSuggestion, setHasSuggestion)
                }}>
                    Find Vacations
                </Button>
                <suggestionsContext.Provider value={{suggestion, setSuggestion}}>
                    {hasSuggestion ? <SuggestedDestination/> : null}
                </suggestionsContext.Provider>
                </body>
            </ThemeProvider>
        </div>
    );
}

export default App;
