# ezproxy
EZProxy developments

## EZProxy default menu page styling

The menu.htm page is shown after login. It is a bit raw by default though it's possible to style and enhance it. In most cases, end users will not see this page if they access to ressources through a direct proxified URL, on rare cases the page might be delivered by the proxy when the url is wrong and the user is logged in. So it's generally not worth the while. But I tried to come up with something nonetheless as a side project while learning JS. Librarian might find usefull to search or sort their database list however.

### Styling

EZProxy manages external CSS and JavaScript so I used Bootsrap 3 to add a minimalist header and footer and make the page responsive. The database list is displayed in a table. See menu-exemple.htm and style.css.

### Sorting, searching, and highlighting

I developed a few Vanilla JS functions to sort, search and highlight the searched string. It can be useful when you have dozens of items (of course CTRL+F does the job).

Here are some screenshot: 

* [Database list](https://accesdistant.sorbonne-universite.fr/public/images/list.png)
* [Database list sorted](https://accesdistant.sorbonne-universite.fr/public/images/sorted.png)
* [Search result](https://accesdistant.sorbonne-universite.fr/public/images/search.png)
* [Small device display](https://accesdistant.sorbonne-universite.fr/public/images/responsive.png)
