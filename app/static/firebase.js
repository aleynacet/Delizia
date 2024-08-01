// benötigten Funktionen aus SDKs importiert
import { initializeApp } from "firebase/app";
import { getAnalytics } from "firebase/analytics";

// Firebase-Konfiguration
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


function registerUser(email, password) {
    return createUserWithEmailAndPassword(auth, email, password);
  }
  

  function loginUser(email, password) {
    return signInWithEmailAndPassword(auth, email, password);
  }

  function logoutUser() {
    return signOut(auth);
  }
  
  export { registerUser, loginUser, logoutUser };