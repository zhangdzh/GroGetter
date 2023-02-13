import logo from './logo.svg';
import './App.css';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <ul>
          <li class="dropdown">
              <a href="index.html">Home</a>
          </li>

          <li class="dropdown">
              <a href="#">Lists</a>
              <div class="dropdown-content">
                  <a href="manageList.html">Manage</a>
                  <a href="addList.html">Add</a>
              </div>
          </li>
        </ul>
      </header>
    </div>
  );
}

export default App;
