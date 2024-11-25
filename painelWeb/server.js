const express = require('express');
const cors = require('cors');              
const mysql = require('mysql2');
const app = express();
const port = 3001;

const db = mysql.createConnection({
    host:"localhost",
    user:"root",
    password:"",
    database:"vagas"
})

app.use(cors());

db.connect(err => {
    if(err){
        throw err;
    }
    console.log('conectado ao banco');

});


app.get('/data',(req,res)=>{
    const query ='SELECT * FROM `vagas_livres` WHERE 1 ';
    db.query(query, (err,result)=>{
        if(err){
            throw err;
        }
        res.json(result);
    })
});

app.listen(port,()=>{
    console.log(`Server running at http://localhost:${port}`)
})