import React, { useEffect, useState } from 'react';
import './App.css';

function App() {
  const [prs, setPrs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedRows, setExpandedRows] = useState({});

  useEffect(() => {
    fetch('http://localhost:5000/api/prs')
      .then(response => {
        if (!response.ok) {
          throw new Error("Erreur HTTP : " + response.status);
        }
        return response.json();
      })
      .then(data => {
        setPrs(data);
        setLoading(false);
      })
      .catch(error => {
        console.error("Erreur lors du fetch :", error);
        setError(error.message);
        setLoading(false);
      });
  }, []);

  const toggleComment = (id) => {
    setExpandedRows(prev => ({
      ...prev,
      [id]: !prev[id]
    }));
  };

  return (
    <div className="App">
      <h1 className="App-title">PR Helper Dashboard</h1>

      {loading ? (
        <p className="App-message">Chargement des Pull Requests...</p>
      ) : error ? (
        <p className="App-error">❌ Erreur : {error}</p>
      ) : prs.length === 0 ? (
        <p className="App-message">🚫 Aucune Pull Request trouvée.</p>
      ) : (
        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Dépôt</th>
                <th>Titre</th>
                <th>Auteur</th>
                <th>Date</th>
                <th>Score</th>
                <th>Statut</th>
                <th>Commentaire</th>
              </tr>
            </thead>
            <tbody>
              {prs.map(pr => (
                <tr key={pr.id}>
                  <td>{pr.id}</td>
                  <td>{pr.repo}</td>
                  <td>{pr.titre}</td>
                  <td>{pr.auteur}</td>
                  <td>{new Date(pr.date).toLocaleString()}</td>
                  <td>{pr.score}</td>
                  <td>{pr.statut}</td>
                  <td>
                    <div className={expandedRows[pr.id] ? '' : 'comment-preview'}>
                      {pr.commentaire}
                    </div>
                    <button className="show-more" onClick={() => toggleComment(pr.id)}>
                      {expandedRows[pr.id] ? 'Masquer' : 'Afficher tout'}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default App;
