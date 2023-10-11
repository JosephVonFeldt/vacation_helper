import {vacationContext} from '../App'
import {css} from '@emotion/css'
import {useContext} from "react";
import ToggleButton from '@mui/material/ToggleButton';
import ToggleButtonGroup from '@mui/material/ToggleButtonGroup';
import Box from "@mui/material/Box";


function VacationTypes() {
    const {selectedVacation, ssv} = useContext(vacationContext);
    const handleChange = (event) => {
        ssv(event.target.value);
    };
//     const ToggleButtonGroup = styled(ToggleButtonGroup)({
//   "&.Mui-selected, &.Mui-selected:hover": {
//     color: "white",
//     backgroundColor: "#cfb87c"
//   }
// });
    return (
        <Box mb={2} pt={3} sx={{width: 220}}>
            <ToggleButtonGroup
                color="primary"
                value={selectedVacation}
                exclusive
                onChange={handleChange}
                aria-label="Vacation-Type"
                sx={{width: 220,}}
            >
                <ToggleButton value="Snow" sx={{width: 73}}>Snow</ToggleButton>
                <ToggleButton value="Beach" sx={{width: 74}}>Beach</ToggleButton>
                <ToggleButton value="Hiking" sx={{width: 73}}>Hiking</ToggleButton>
            </ToggleButtonGroup>
        </Box>

    );
}

export default VacationTypes;