import './App.css';
import axios from "axios";
import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

function App() {
  const [artist, setArtist] = useState("")
  const [info, setInfo] = useState({})
  const navigate = useNavigate()

  const search_artist = async() => {
    console.log("searching for artist")
    await axios.get(
      `https://ncoztkt0v6.execute-api.us-east-2.amazonaws.com/dev/lyrr-backend/artist?artist_name=${artist}`
    )
    .then((res) => {
      console.log(res['body'])
      setInfo(res['body'])
    })
    .catch((err) => {
      console.log(err)
      alert("Something has gone wrong :( please try again")
    })
    // await axios.get(`http://127.0.0.1:5000/artist?artist_name=${artist}`)
    // .then((res) => {
    //   console.log(res['data'])
    //   setInfo(res['data']['artist'])
    // })
  }

  const select_artist = () => {
    if (info.exists) {
      navigate(`/lyrics`, { state: { id: info.id, artist: info.name } })
    } else {
      alert('artist does not exist');
    }
  }

  const handlePress = (e) => {
    if(e.key === 'Enter') { 
      search_artist()
    }
  }

  return (
    <div className="App">
        <div className="title">
            LYRR
        </div>
        enter artist name: 
        <input type="text" onChange={(e) => setArtist(e.target.value)} className="input" 
            onKeyDown={(e) => handlePress(e)}
        />
        <button onClick={() => search_artist()} className="button">search</button>
        {(() => {
          if (Object.keys(info).length !== 0) {
            return (
              <div className="found_artist">
                <img src={info.image} className="artist_img" alt="img"/>
                <p>{info.name}</p>
                <button className="button" onClick={() => select_artist()}>select</button>
              </div>
            )
          }
        })()}
    </div>
  );
}

export default App;
