function autocomplete(inp, arr) {
  /*the autocomplete function takes two arguments,
  the text field element and an array of possible autocompleted values:*/
  var currentFocus;
  /*execute a function when someone writes in the text field:*/
  inp.addEventListener("input", function(e) {
      var a, b, i, val = this.value;
      /*close any already open lists of autocompleted values*/
      closeAllLists();
      if (!val) { return false;}
      currentFocus = -1;
      /*create a DIV element that will contain the items (values):*/
      a = document.createElement("DIV");
      a.setAttribute("id", this.id + "autocomplete-list");
      a.setAttribute("class", "autocomplete-items");
      /*append the DIV element as a child of the autocomplete container:*/
      this.parentNode.appendChild(a);
      /*for each item in the array...*/
      for (i = 0; i < arr.length; i++) {
        /*check if the item starts with the same letters as the text field value:*/
        if (arr[i].substr(0, val.length).toUpperCase() == val.toUpperCase()) {
          /*create a DIV element for each matching element:*/
          b = document.createElement("DIV");
          /*make the matching letters bold:*/
          b.innerHTML = "<strong>" + arr[i].substr(0, val.length) + "</strong>";
          b.innerHTML += arr[i].substr(val.length);
          /*insert a input field that will hold the current array item's value:*/
          b.innerHTML += "<input type='hidden' value='" + arr[i] + "'>";
          /*execute a function when someone clicks on the item value (DIV element):*/
          b.addEventListener("click", function(e) {
              /*insert the value for the autocomplete text field:*/
              inp.value = this.getElementsByTagName("input")[0].value;
              /*close the list of autocompleted values,
              (or any other open lists of autocompleted values:*/
              closeAllLists();
          });
          a.appendChild(b);
        }
      }
  });
  /*execute a function presses a key on the keyboard:*/
  inp.addEventListener("keydown", function(e) {
      var x = document.getElementById(this.id + "autocomplete-list");
      if (x) x = x.getElementsByTagName("div");
      if (e.keyCode == 40) {
        /*If the arrow DOWN key is pressed,
        increase the currentFocus variable:*/
        currentFocus++;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 38) { //up
        /*If the arrow UP key is pressed,
        decrease the currentFocus variable:*/
        currentFocus--;
        /*and and make the current item more visible:*/
        addActive(x);
      } else if (e.keyCode == 13) {
        /*If the ENTER key is pressed, prevent the form from being submitted,*/
        e.preventDefault();
        if (currentFocus > -1) {
          /*and simulate a click on the "active" item:*/
          if (x) x[currentFocus].click();
        }
      }
  });
  function addActive(x) {
    /*a function to classify an item as "active":*/
    if (!x) return false;
    /*start by removing the "active" class on all items:*/
    removeActive(x);
    if (currentFocus >= x.length) currentFocus = 0;
    if (currentFocus < 0) currentFocus = (x.length - 1);
    /*add class "autocomplete-active":*/
    x[currentFocus].classList.add("autocomplete-active");
  }
  function removeActive(x) {
    /*a function to remove the "active" class from all autocomplete items:*/
    for (var i = 0; i < x.length; i++) {
      x[i].classList.remove("autocomplete-active");
    }
  }
  function closeAllLists(elmnt) {
    /*close all autocomplete lists in the document,
    except the one passed as an argument:*/
    var x = document.getElementsByClassName("autocomplete-items");
    for (var i = 0; i < x.length; i++) {
      if (elmnt != x[i] && elmnt != inp) {
        x[i].parentNode.removeChild(x[i]);
      }
    }
  }
  /*execute a function when someone clicks in the document:*/
  document.addEventListener("click", function (e) {
      closeAllLists(e.target);
  });
}

/*initiate the autocomplete function on the "myInput" element, and pass along the countries array as possible autocomplete values:*/
// autocomplete(document.getElementById("meal"), countries);
// var meal_list = ['Caprese', 'Carbonara', 'Tonno', 'Pizza', 'Avocado Feta e pomodorini', 'Stracchino e pomodorini', 'Mozzarella', 'Coso', 'Melone prosciutto e piada', 'Risotto agli agrumi', 'Erbazzone', 'Pennette salmone e vodka', 'Norma di pesce spada', 'Uova alla trentina', 'Tortellata', 'Ricotta', 'Tagliolini al salmone', 'Tomini in sfoglia', 'Piada e pesca', 'Bastoncini findus', 'Lasagne', 'Avanzi', 'Bacon Bomb', 'Calamari ripieni', 'Rucola Feta Pere e noci', 'Costine e patate', 'Crostini salsiccia e stracchino', 'Tramezzini', 'Pasta Gorgonzola Speck e Noci', 'Uova strapazzate', 'Ricotta e Formaggi', 'Prosciutto e melone', 'Pasta peperoni e feta', 'Insalata Feta Pere e Noci', 'Asado con patate', 'Risotto stracciatella melanzana pom secchi', 'Piade varie', 'Crostini stracchino e salsiccia', 'Pasta feta e peperoni', 'Taralli e Mascarpone', 'Burrata e pepppeleone', 'Uova alla contadina', 'Persico gratinato', 'Camomilla e piada', 'Zuppa Scipole', 'Uova speck e patate', 'Brodino', 'Riso venere zucchine salmone mascarpone ', 'Insalatone pere grana e noci', 'Tigellata', 'Insalata pomodi mozzarella e tonno', 'Calamarata', 'Insalata finocchio arancia e uvetta', 'Melone feta e piada', 'Tonno pomodorini e mozzarella', "L'aquila nera", 'Filetti di trota glacé', 'Tomini in pasta sfoglia', 'Avanzi (piada stracchino e insalata, stracciatella e melone) ', 'Risotto fonduta parmigiano e pancetta', 'Pasta al forno radicchio, Scamorza e besciamella', 'Cotechino purè lenticchie', 'Fregola con ragù di agnello + dolce mattone', 'Panini/piadine salsiccia', 'Norma di spada', 'Kebab', 'Radicchio gratinato', 'Pesce gratinato', 'Risotto Traminer mele e noci', 'Frittata scipole', 'Tartare Salmone e avocado, voulevant salmone e philadelphia', 'Cacio e pepe', 'Spaghetti Stracciatella melanzane grigliate e mandorle', 'Avanzi insalata', 'Zucchine e limone', 'Carne salada e fagioli', 'Frittata pepppeloni cipolla', 'Giro birrerie!', 'Ubriaca', 'Pasta feta e pepppelone', 'Pizzeria', 'Ricotta e noci', 'Ristorante (Giardino delle spezie)', 'Carbonara asparagi', 'Piada Mozzarella finocchio', 'Seppie e gamberoni alla griglia', 'Tomini + Pepppelone', 'Omelette funghi e formaggio', 'Tigelle + Pepppelone', 'Insalata, melone, stracciatella', 'Polpette al sugo', 'Gamberetti in sfoglia', 'Parmigiana', 'Rifugio Agostini', 'Involtini alla siciliana', 'Insalata avocado Feta e pomodorini ', 'Pollo agli agrumi', 'Sfornato cotto e sottiletta', 'Lasagne + Mozzarella e tonno', 'Rotolo funghi speck e formaggio', 'Melanzane grigliate + Pepppelone + Ricotta', 'Tonno e mozzarella', 'Risotto salmone zucchine e mascarpone', 'Filetti trota glacé', 'Pomodori ripieni riso', 'Agritur le Vallene', 'Insalata feta e peperoni ', 'Thè e piada scarsa', 'Tomini', 'Insalata pomodorini caprino e noci', 'Pochi avanza', 'Peperonata', 'Grigliata Marzola', 'Pollo alle mandorle', 'Filetti glasse ', 'Piada e mozzarella', 'Hamburger e patatine fritte', 'Mucchio', 'Melanzane grigliate e pepppelone', 'Melone ', 'Crostini di salsiccia e stracchino', 'Cous cous Feta', 'Fagiolatina', 'Insalata arancia finocchio pomodoro', 'Melanzane grigliate e burrata', 'Cous cous', 'Mozzarella e tonno', 'Piada ', 'Sushi', 'Tartare rucola e pomodorini ', 'Salmone al miele', 'Terrina di pane funghi spinaci']
autocomplete(document.getElementById("meal"), meal_list);