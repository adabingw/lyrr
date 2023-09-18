import './App.css';
import axios from "axios";
import { useLocation } from 'react-router-dom';
import { useState, useEffect } from 'react';
import MenuItem from '@mui/material/MenuItem';
import {ReactSpinner} from 'react-spinning-wheel';
import 'react-spinning-wheel/dist/style.css';

function Generate() {
  let { state } = useLocation();
  let { artist, id } = state;
  const [text, setText] = useState("")
  const [lyrics, setLyrics] = useState("")
  const [show, setShow] = useState(false)

  const get_lyrics = async() => {
    let artist_name = artist.replace(" ", "").toLowerCase();
    setLyrics('')
    setShow(true)
    console.log("artist name: ", artist_name)
    await axios.post(`http://127.0.0.1:5000/lyrics?lyrics=${text}&artist=${artist_name}`)
    .then((res) => {
      console.log(res['data'])
      setLyrics(res['data']['lyrics'])
    })
    .catch((err) => {
        console.log(err)
        alert("Something has gone wrong :( please try again")
        setShow(false) 
        setLyrics('')
    })
  }

  return (
    <div className="App">
    {/* route back to home */}
        <div className="title"> 
          LYRR
        </div>
        <p>{artist}</p>
        start with something:
        <input onChange={(e) => setText(e.target.value)} className="lyric-input" maxLength={25}/> <br />
        <button onClick={get_lyrics} className="get-lyrics" disabled={text.length === 0}>
              get lyrics
        </button>
        <div className="lyrics">
            {lyrics}
        </div>
        <div className="spinner">
          { show && lyrics === '' &&
              <ReactSpinner />
          }
        </div>
    </div>
  );
}

export default Generate;
