import './App.css'
import {useEffect, useRef, useState} from 'react';
import {render} from "react-dom";

function App() {

  const [url, setUrl] = useState<string>();
  const [email, setEmail] = useState<string>();

  useEffect(() => {
    const f = async () => {
      const url = await fetch('http://localhost:8000/get_auth_url').then(e => e.json())
      setUrl(url.result);
      if (document.location.pathname === '/oauth-callback') {
        const params = new URLSearchParams(document.location.search);
        const res = await fetch('http://localhost:8000/oauth-callback/?' + params, {method: "POST"}).then(e => e.json())
        console.log(res)
        const res2 = await fetch('http://localhost:8000/get_me/?' + new URLSearchParams(res)).then(e => e.json())
        setEmail(res2.email)
      }
    }

    f()
  }, [])

  return <div>
    <a href={url}>ВОЙТИ</a>
    {email && <span>
        Вы вошли как {email}
    </span>}
  </div>
}

export default App
