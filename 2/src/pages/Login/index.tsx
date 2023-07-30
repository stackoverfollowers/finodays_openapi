import React, {useState} from 'react';
import {getAuth, signInWithEmailAndPassword} from "firebase/auth";
import styles from './Login.module.scss'

const auth = getAuth();

interface LoginProps {

}

export function Login({}: LoginProps) {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');


  const login = async () => {
    try {
      const userCredential = await signInWithEmailAndPassword(auth, email, password);
    } catch (e) {
      console.log(e)
    }
  }

  return (
    <div>
      <label><input value={email} onChange={event => setEmail(event.target.value)}/>EMAIL</label>
      <label><input value={password} onChange={event => setPassword(event.target.value)}/>PASSWORD</label>
      <button onClick={login}>Войти</button>
    </div>
  )
}
