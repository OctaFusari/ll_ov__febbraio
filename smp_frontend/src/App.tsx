import React, { useState } from "react";
import axios from "axios";
import "./App.css";

const App = () => {
  const [nomeAzienda, setNomeAzienda] = useState("");
  const [modelType, setTipoModello] = useState("");
  const [result, setResult] = useState({
    prediction: [{}],
    compagnia: "",
    errore: "",
  });
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

          setResult({
            prediction: response.data.prediction,
            compagnia: response.data.company,
            errore: "",
          });
          console.log(response.data);
        });
    } catch (error) {
      console.error("Errore nella richiesta:", error);
      setResult({
        prediction: [{}],
        compagnia: "",
        errore: "C'è stato un errore durante il recupero dei dati",
      });
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px", fontFamily: "Arial" }}>
      <div>
        <h1>SMP</h1>
        <p>
          Previsione dell'andamento delle aziende attraverso la sentiment
          analysis
        </p>
      </div>

      <div className="grid__centrale">
        <div className="container">
          <form onSubmit={chimata__smp__backend}>
            <div>
              <h2>
                <label htmlFor="nomeAzienda">CIK azienda: </label>
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
            <h2>Seleziona il tipo di modello</h2>

            <div>
              <label>
                <input
                  type="radio"
                  value="svm"
                  checked={modelType == "svm"}
                  onChange={handleModelChange}
                />
                Modello basato su SVC
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
            <button
              type="submit"
              style={{ marginTop: "10px", padding: "5px 10px" }}
            >
              Fai previsione
            </button>
          </form>
        </div>
        {loading ? (
          <div className="spinner"></div> // Mostra lo spinner mentre carica
        ) : (
          <div className="container">
            <h2>Nome della compagnia</h2>
            <p>{result.compagnia || "nessun risultato ancora"}</p>
            <div>
            <ul>
              {result.prediction.map((item, index) => (
                <li key={index}>
                  {item.news} - Sentiment: {item.sentiment}
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
