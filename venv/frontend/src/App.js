import './App.css';
import axios from "axios";
import { useState, useEffect } from 'react';
import MenuItem from '@mui/material/MenuItem';
import FormControl from '@mui/material/FormControl';
import Select from '@mui/material/Select';

function App() {
  const [text, setText] = useState("")
  const [lyrics, setLyrics] = useState("")
  const [models, setModels] = useState([])
  const [artist, setArtist] = useState(0)

  useEffect(() => {
    axios.post(`http://127.0.0.1:5000/select`)
    .then((res) => {
      console.log(res['data'])
      setModels(res['data']['models'])
    })
    .catch((err) => {
        console.log(err)
    })
  }, [])

  const get_lyrics = async() => {
    await axios.post(`http://127.0.0.1:5000/lyrics?lyrics=${text}&artist=${artist}`)
    .then((res) => {
      console.log(res['data'])
      setLyrics(res['data']['lyrics'])
    })
    .catch((err) => {
        console.log(err)
    })
  }

  return (
    <div className="App">
      <div className="title">
        LYRR
      </div>
        <FormControl sx={{ m: 1, minWidth: 300 }} >
          <Select
            value={artist}
            displayEmpty
            inputProps={{ 'aria-label': 'Without label' }}
            onChange={(e) => {setArtist(e.target.value)}}
            sx={{
                minWidth: "300px",
                height: "35px",
                "& .MuiSelect-select": {
                  padding: "0.2rem"
                },
                ".MuiOutlinedInput-notchedOutline": {
                  borderColor: "#454545 !important"
                }
            }}
          >
            {models.map((model, index) => {
              return (
                <MenuItem value={index}>{model}</MenuItem>
              )
            })}
          </Select>
        </FormControl> <br />
        <input onChange={(e) => setText(e.target.value)} className="lyric-input" maxLength={25}/> <br />
        <button onClick={get_lyrics} className="get-lyrics" disabled={text.length === 0}>
              get lyrics
        </button>
        <div className="lyrics">
            {lyrics}
        </div>
    </div>
  );
}

export default App;
