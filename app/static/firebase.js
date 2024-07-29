// Importieren Sie die benötigten Funktionen aus den SDKs, die Sie benötigen
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

// Die Firebase-Konfiguration Ihrer Web-App
// Für Firebase JS SDK v7.20.0 und später ist measurementId optional
const firebaseConfig = {
  apiKey: "AIzaSyA6v-GqDEwprY98nShBwTJRJTbvQrXc0iA",
  authDomain: "delizia-cc6d1.firebaseapp.com",
  projectId: "delizia-cc6d1",
  storageBucket: "delizia-cc6d1.appspot.com",
  messagingSenderId: "185123758782",
  appId: "1:185123758782:web:404092ef3b4a4069b3b4ef",
  measurementId: "G-4WXTC6V3WH"
};

// Firebase initialisieren
const app = initializeApp(firebaseConfig);
const analytics = getAnalytics(app);

// Function to register user
function registerUser(email, password) {
    return createUserWithEmailAndPassword(auth, email, password);
  }
  
  // Function to login user
  function loginUser(email, password) {
    return signInWithEmailAndPassword(auth, email, password);
  }
  
  // Function to logout user
  function logoutUser() {
    return signOut(auth);
  }
  
  export { registerUser, loginUser, logoutUser };