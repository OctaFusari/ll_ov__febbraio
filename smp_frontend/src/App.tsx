import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [nomeAzienda, setNomeAzienda] = useState("");
  const [modelType, setTipoModello] = useState("");
  const [result, setResult] = useState([]);
  const [loading, setLoading] = useState(false);

  const handleModelChange = (event: any) => {
    setTipoModello(event.target.value);
  };

  const chimata__smp__backend = async (e: any) => {
    e.preventDefault();
    setLoading(true);

    console.log(nomeAzienda, modelType)
    try {
      await axios
        .post("http://127.0.0.1:8000/", {
          name: nomeAzienda,
          model: modelType,
        })
        .then((response) => {
          setLoading(false);

          setResult(response.data);
          console.log(response.data);
        });
    } catch (error) {
      console.error("Errore nella richiesta:", error);
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>

      <div className="grid__centrale">
        <div>
          <div className="container container__ricerca">  
          <div>
            <h1>News sentiment</h1>
            <p>
              Previsione dell'andamento delle aziende attraverso la sentiment
              analysis
            </p>
          </div>
          <form onSubmit={chimata__smp__backend}>
            <div className="container">
              <h2>
                <label htmlFor="nomeAzienda">Nome azienda: </label>
              </h2>
              <input
                type="text"
                id="nomeAzienda"
                value={nomeAzienda}
                onChange={(e) => setNomeAzienda(e.target.value)}
                placeholder="Nome azienda"
                style={{ marginLeft: "10px", padding: "5px" }}
              />
            </div>
            <div  className="container">
            <h2>Seleziona il tipo di modello</h2>

            <div>
              <label>
                <input
                  type="radio"
                  value="svc"
                  checked={modelType == "svc"}
                  onChange={handleModelChange}
                />
                Modello basato su svc
              </label>
            </div>

            <div>
              <label>
                <input
                  type="radio"
                  value="rf"
                  checked={modelType == "rf"}
                  onChange={handleModelChange}
                />
                Modello basato su Random Forest
              </label>
            </div>

</div>
            <button
              type="submit"
            >
              Fai previsione
            </button>
          </form>
        </div>
            
            </div>
        {loading ? (
          <div className="spinner"></div> // Mostra lo spinner mentre carica
        ) : (
          <div className="container container__results">
            <h2>Risultato {nomeAzienda}</h2>
            <div>
              <ul>
                {result.map((item, index) => (  
                  <li className="container" key={index}>
                    <h2>{item["title"]}</h2>
                    <div>
                      <h3>{item["sentiment"]}</h3>
                      <a href={item['link']} target="_blank" rel="noopener noreferrer">Link articolo</a>
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
