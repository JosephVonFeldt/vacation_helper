import {useContext} from 'react';
import {airportContext} from '../App'
function DepartureList(props) {
  const {selectedAirport, setSelectedAirport} = useContext(airportContext);
  return (
    <div className="DepartureList">
        <select id="Departure-City" value={selectedAirport} onChange={e => setSelectedAirport(e.target.value)}>
            <option></option>
            {props.cities.map((key, i) => {
                return <option  key={i} value={key.AP}>{key.CITY}</option>;
            })}
        </select>
    </div>
  );
}

export default DepartureList;