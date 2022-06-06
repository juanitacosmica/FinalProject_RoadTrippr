// import { initializeApp } from "https://www.gstatic.com/firebasejs/9.8.1/firebase-app.js";
// import { doc, setDoc } from "https://www.gstatic.com/firebasejs/9.8.1/firebase-firestore.js";
// import { getDatabase, ref, set } from "https://www.gstatic.com/firebasejs/9.8.1/firebase-database.js";
// import { getAuth } from "https://www.gstatic.com/firebasejs/9.8.1/firebase-auth.js";

// const firebaseConfig = {
//   apiKey: "AIzaSyAizKiBWMmyxDAF9BkJFTfsk8VnEXzCnnQ",
//   authDomain: "trippr-62b9f.firebaseapp.com",
//   databaseURL: "https://trippr-62b9f-default-rtdb.firebaseio.com",
//   projectId: "trippr-62b9f",
//   storageBucket: "trippr-62b9f.appspot.com",
//   messagingSenderId: "836402456269",
//   appId: "1:836402456269:web:3fd354f16e2d5f84d8ab84",
//   measurementId: "G-MN1VTEJYGM"
// };

// // Initialize Firebase
// const app = initializeApp(firebaseConfig);
// const database = getDatabase(app);
// const auth = getAuth();

// function handaleSubmmit (event) {
//   event.preventDefault();
//   var radioboxes = document.getElementsByClassName('qAns');
//   var radioanswers = [];
//   var radiodict = {};
//   for(var i=0; i<radioboxes.length; i++){
//     if(radioboxes[i].checked == true){
//       radioanswers.push(radioboxes[i].id);
//     }  
//   }

//   radiodict["question 01"] = radioanswers[0];
//   radiodict["question 02"] = radioanswers[1];
//   radiodict["question 03"] = radioanswers[2];
//   radiodict["question 04"] = radioanswers[3];
//   radiodict["question 05"] = radioanswers[4];
//   radiodict["question 06"] = radioanswers[5];
//   radiodict["question 07"] = radioanswers[6];
//   radiodict["question 08"] = radioanswers[7];
//   radiodict["question 09"] = radioanswers[8];
//   radiodict["question 10"] = radioanswers[9];

//   console.log(radiodict);

//   // const user = auth.currentUser;
//   // console.log("user="+user);
//   // if(user){
//   //   var id = user.uid;
//   //   console.log(id);
//   // }else{
//   //   console.log("no login");
//   // }  
// }

