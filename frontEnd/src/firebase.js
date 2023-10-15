import { initializeApp } from "firebase/app";
import { getFirestore } from "firebase/firestore";

const config = {
  apiKey: "AIzaSyBCqTfnnW1K89DZvF1NlEO1_yvQgWaZ8Hk",
  authDomain: "test-6d4f5.firebaseapp.com",
  databaseURL: "https://test-6d4f5-default-rtdb.firebaseio.com",
  projectId: "test-6d4f5",
  storageBucket: "test-6d4f5.appspot.com",
  messagingSenderId: "581435201389",
  appId: "1:581435201389:web:67a158db39935ec788ec64",
  measurementId: "G-NYZ8SX222M"
};

export default getFirestore(initializeApp(config));

