import {suggestionsContext} from '../App'
import {useContext} from "react";

function SuggestedDestination() {
  const {suggestion, setSuggestion} = useContext(suggestionsContext);
  return (
    <div className="Suggestion">
      {suggestion.map((key, i) => {
        if (key.POSSIBLE){
          return <div>
            { key.CITY } $ {key.PRICE}<a href={key.LINK}>link</a>
          </div>;
        }
      })}
    </div>
  );
}

export default SuggestedDestination;