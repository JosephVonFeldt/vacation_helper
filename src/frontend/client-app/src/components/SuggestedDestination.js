import {suggestionsContext} from '../App'
import {useContext} from "react";
import {List, ListItem, ListItemButton, ListItemText} from "@mui/material";

function SuggestedDestination() {
    const {suggestion} = useContext(suggestionsContext);
    return (
        <div className="Suggestion">
            {suggestion.filter(key => {
                return key.POSSIBLE
            }).length > 0 ?
                < List sx={{
                    '& .MuiListItemButton-root:hover': {
                        bgcolor: 'rgba(0,0,0,0.3)',
                    },
                }}>{suggestion.map((key, i) => {
                    if (key.POSSIBLE) {
                        return <ListItem>
                            <ListItemButton component="a" href={key.LINK}
                                            sx={{border: 1, borderRadius: 4, backgroundColor: '#000000'}}>
                                <ListItemText primary={key.CITY + ' $' + key.PRICE}/>
                            </ListItemButton>
                        </ListItem>;
                    }
                })} </List> :
                <div>No Results</div>}
        </div>
    );
}

export default SuggestedDestination;