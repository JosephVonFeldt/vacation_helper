import {useContext} from 'react';
import {airportContext} from '../App'
import FormControl from "@mui/material/FormControl";
import InputLabel from "@mui/material/InputLabel";
import Select from "@mui/material/Select";
import {css} from "@emotion/css";
import MenuItem from "@mui/material/MenuItem";
import Box from "@mui/material/Box";

function DepartureList(props) {
    const {selectedAirport, ssa} = useContext(airportContext);
    const handleChange = (event) => {
        ssa(event.target.value);
    };
    return (
        <Box mt={2} pt={3} sx={{width: 220 } }>
            <FormControl fullWidth>
                <InputLabel id="dep-city-select-label">Departure City</InputLabel>
                <Select
                    labelId="dep-city-select-label"
                    id="dep-city-select"
                    value={selectedAirport}
                    label="Departure City"
                    onChange={handleChange}
                >
                    <MenuItem></MenuItem>
                    {props.cities.map((key, i) => {
                        return <MenuItem key={i} value={key.AP}>{key.CITY}</MenuItem>;
                    })}
                </Select>
            </FormControl>
        </Box>
    );
}

export default DepartureList;