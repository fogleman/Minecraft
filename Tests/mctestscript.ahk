arr := ["w", "a", "s", "d","Lbutton","Rbutton","Space"]

$q::
sendinput % {w DOWN}
sleep 100
sendinput % {w UP}
sendinput % {a DOWN}
sleep 100
sendinput % {a UP}
sendinput % {s DOWN}
sleep 100
sendinput % {s UP}
sendinput % {d DOWN}
sleep 100
sendinput % {d UP}
MouseMove, 0, 60, 50, R
sendinput % {Lbutton DOWN}
sleep 100
sendinput % {Lbutton UP}
MouseMove, 800, -60, 50, R
sendinput % {w DOWN}
sleep 500
sendinput % {w UP}
MouseMove, 0, 60, 50, R
sendinput % {Lbutton DOWN}
sleep 100
sendinput % {Lbutton UP}
sendinput % {Rbutton DOWN}
sleep 100
sendinput % {Rbutton UP}

loop 300
{
Random, oVar, 65, 122						
sendinput % {chr(oVar) DOWN}
sleep 100
sendinput % {chr(oVar) UP}
}
loop 1000
{
Random, oVar, 1, 7						
sendinput % {arr[oVar] DOWN}
sleep 100
sendinput % {arr[oVar] UP}
}
return