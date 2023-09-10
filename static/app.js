const loading  = document.getElementsByClassName("loading")[0];

window.addEventListener('load', () => {
    loading.style.animation = "fade ease 1s forwards";
    setTimeout(() => {
        loading.classList.add("hide")
    }, 1000)
})


const links = document.querySelectorAll('.link');
links.forEach((l, i) => l.addEventListener("click", (e) => {
    localStorage.clear();
    localStorage.setItem("link",i);
}))
l = localStorage.getItem("link") || 0;
links[l].style.color = "#fff"


const btn = document.getElementsByClassName("sbtn")[0];
const popup = document.getElementsByClassName("popCont")[0];
const note = document.getElementsByClassName("note")[0];
const back = document.getElementsByClassName("header")[0];

const cards = document.getElementsByClassName("cards")[0];
const bg = document.querySelectorAll(".bg");
const dbtn = document.querySelectorAll(".dbtn");


btn.addEventListener("click", () => {istart()})

back.addEventListener("click", () => {istop()})

let setIVal = 0;
dbtn.forEach((btn, i) => {
    btn.addEventListener("click", () => {
        setIVal = i;
        toggle(cards, bg[i])
    })
})

const istart = () => {
    toggle(note, popup)
}

const istop = () => {
    bg.forEach((b) => {
        toggle(b, cards)
    })
}

const toggle = (f,s) => {
    f.classList.add("hide");
    s.classList.remove("hide");
}


const inputs = document.querySelectorAll(".query");
const tags = document.querySelectorAll(".tag");
let collections = [];



tags.forEach((tag, i) => {
    inputs[setIVal].value = "";
    tag.addEventListener("click", (e) => {
        let state = false;
        const changeState = (coll) => {if(coll == tag.textContent){state = true;}}
        if(tag.classList[tag.classList.length - 1] === "selected"){
            tag.classList.remove("selected")
            collections.map((coll) => {changeState(coll)})
            if(state){
                let ind = collections.indexOf(tag.textContent)
                collections.splice(ind, 1);
                writeInp();
            }
        }else{
            if(setIVal === inputs.length-1){
                if(collections.length > 0){
                    collections.map((coll) => {changeState(coll)})
                    if(!state){
                        collections.push(tag.textContent);
                    }
                }else{
                    collections.push(tag.textContent);
                }
                writeInp()
            }else{
                tags.forEach(t => t.classList.remove("selected"))
                inputs[setIVal].value = tag.textContent;
            }
            tag.classList.add("selected")
        };

    })
})

const writeInp = () => {
    inputs[setIVal].value = "";
    collections.map((col) => {
        inputs[setIVal].value += `${col},`;
    })
}


