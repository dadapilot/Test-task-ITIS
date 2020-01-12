function questions()

{
if(document.getElementById("q1").checked)
    {
    document.getElementById("date").style.display="none";
    document.getElementById("categories").style.display="none";
    }
else if (document.getElementById("q2").checked)
    {
     document.getElementById("categories").style.display="block";
     document.getElementById("date").style.display="none";
    }
else {
    document.getElementById("categories").style.display = "none";
    document.getElementById("date").style.display = "block";
    }
}

