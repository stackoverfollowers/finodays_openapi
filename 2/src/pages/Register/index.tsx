import React, {useState} from 'react';
import {getAuth, createUserWithEmailAndPassword} from "firebase/auth";
import styles from './Register.module.scss'

const auth = getAuth();

export function Register() {
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');

  const register = async () => {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
    } catch (e) {
      console.log(e)
    }
  }

  return (
    <div>
      <label><input value={email} onChange={event => setEmail(event.target.value)}/>EMAIL</label>
      <label><input value={password} onChange={event => setPassword(event.target.value)}/>PASSWORD</label>
      <button onClick={register}>Регистрация</button>
    </div>
  )
}
