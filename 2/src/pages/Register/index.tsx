import React, {useContext, useState} from 'react';
import {createUserWithEmailAndPassword} from "firebase/auth";
import styles from './Register.module.scss'
import {auth} from "../../main";
import {NavLink, useNavigate} from "react-router-dom";
import {Context} from "../../App";

export function Register() {
  const {setUser} = useContext(Context)
  const [email, setEmail] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const navigate = useNavigate();

  const register = async () => {
    try {
      const userCredential = await createUserWithEmailAndPassword(auth, email, password);
      setUser(userCredential);
      navigate('/');
    } catch (e) {
      console.log(e)
    }
  }

  return (
    <div className={styles.container}>
      <label><input value={email} onChange={event => setEmail(event.target.value)}/>EMAIL</label>
      <label><input value={password} onChange={event => setPassword(event.target.value)}/>PASSWORD</label>
      <button onClick={register}>Регистрация</button>
      <NavLink to='/login'>Войти</NavLink>
    </div>
  )
}
