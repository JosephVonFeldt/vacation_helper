import {vacationContext} from '../App'
import {useContext} from "react";

function VacationTypes() {
  const {selectedVacation, setSelectedVacation} = useContext(vacationContext);
  return (
    <div className="VacationTypes">
        <input  type="radio" value="Snow" id="Snow" name="vacation" className="VacationType" checked={selectedVacation==='Snow'}
                onChange={(event)=>(setSelectedVacation(event.target.value))}/>
        <label htmlFor="Snow">Snow</label>
        <input  type="radio" value="Hiking" id="Hiking" name="vacation" className="VacationType" checked={selectedVacation==='Hiking'}
                onChange={(event)=>(setSelectedVacation(event.target.value))}/>
        <label htmlFor="Hiking">Hiking</label>
        <input  type="radio" value="Beach" id="Beach" name="vacation" className="VacationType" checked={selectedVacation==='Beach'}
                onChange={(event)=>(setSelectedVacation(event.target.value))}/>
        <label htmlFor="Beach">Beach</label>
    </div>
  );
}

export default VacationTypes;