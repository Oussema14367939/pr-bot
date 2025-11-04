// src/pages/Dashboard.jsx
import React, { useEffect, useState } from "react";
import {
  PieChart, Pie, Cell, Tooltip, Legend,
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  LineChart, Line
} from "recharts";
import { FaChevronLeft, FaChevronRight } from "react-icons/fa";


export default function Dashboard() {
  const [prs, setPrs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [expandedRows, setExpandedRows] = useState({});
  const [filterStatus, setFilterStatus] = useState("all");

  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 5;

  useEffect(() => {
    fetch("http://localhost:5000/api/prs")
      .then((res) => {
        if (!res.ok) throw new Error("Erreur HTTP : " + res.status);
        return res.json();
      })
      .then((data) => {
        setPrs(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error("Erreur lors du fetch :", err);
        setError(err.message);
        setLoading(false);
      });
  }, []);

  const toggleComment = (id) => {
    setExpandedRows((prev) => ({
      ...prev,
      [id]: !prev[id],
    }));
  };

  const normalizeStatus = (status) => {
    if (!status && status !== 0) return "";
    let s = String(status).trim().toLowerCase();
    s = s.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
    s = s.replace(/[^a-z0-9\s]/g, "");
    s = s.replace(/\s+/g, " ").trim();
    return s;
  };

  const getStatusKey = (status) => {
    const norm = normalizeStatus(status);
    if (norm.includes("approuv") || norm.includes("approve") || norm.includes("approved")) {
      return "approved";
    }
    if (
      norm.includes("revis") ||
      norm.includes("a reviser") ||
      norm.includes("changes") ||
      norm.includes("change") ||
      norm.includes("requested") ||
      norm.includes("review")
    ) {
      return "toReview";
    }
    return "other";
  };

  const totalPRs = prs.length;
  let approvedCount = 0;
  let toReviewCount = 0;
  let otherCount = 0;
  let sumScore = 0;

  prs.forEach((pr) => {
    const key = getStatusKey(pr.statut);
    if (key === "approved") approvedCount++;
    else if (key === "toReview") toReviewCount++;
    else otherCount++;
    sumScore += pr.score ? Number(pr.score) : 0;
  });

  const avgScore = totalPRs > 0 ? (sumScore / totalPRs).toFixed(2) : 0;

  const filteredPRs = prs.filter((pr) => {
    const key = getStatusKey(pr.statut);
    if (filterStatus === "all") return true;
    return key === filterStatus;
  });

  const totalPages = Math.ceil(filteredPRs.length / itemsPerPage);
  const paginatedPRs = filteredPRs.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  const handlePrevPage = () => {
    setCurrentPage((prev) => Math.max(prev - 1, 1));
  };

  const handleNextPage = () => {
    setCurrentPage((prev) => Math.min(prev + 1, totalPages));
  };

  const pieData = [
    { name: "Approuvées", value: approvedCount },
    { name: "À réviser", value: toReviewCount },
    { name: "Autres", value: otherCount },
  ];

  const barData = pieData;

  const lineData = prs.map((pr) => ({
    name: `PR ${pr.id}`,
    score: Number(pr.score) || 0,
  }));

  const COLORS = ["#4CAF50", "#FFC107", "#9E9E9E"];

  return (
    <div className="p-6 bg-gray-900 min-h-screen">
      <h1 className="text-3xl font-bold text-white mb-6">📊 PR Helper Dashboard</h1>

      {/* Cartes de statistiques */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4 mb-6">
        <StatCard title="Total PR" value={totalPRs} color="bg-blue-500" onClick={() => setFilterStatus("all")} active={filterStatus === "all"} />
        <StatCard title="Approuvées" value={approvedCount} color="bg-green-500" onClick={() => setFilterStatus("approved")} active={filterStatus === "approved"} />
        <StatCard title="À réviser" value={toReviewCount} color="bg-yellow-500" onClick={() => setFilterStatus("toReview")} active={filterStatus === "toReview"} />
        <StatCard title="Autres" value={otherCount} color="bg-gray-500" onClick={() => setFilterStatus("other")} active={filterStatus === "other"} />
        <StatCard title="Score moyen" value={avgScore} color="bg-purple-500" disabled />
      </div>

      {/* Graphiques */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mb-6">
        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Répartition des PR</h2>
          <PieChart width={300} height={300}>
            <Pie data={pieData} cx="50%" cy="50%" outerRadius={100} label>
              {pieData.map((entry, index) => (
                <Cell key={index} fill={COLORS[index % COLORS.length]} />
              ))}
            </Pie>
            <Tooltip />
            <Legend />
          </PieChart>
        </div>

        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Nombre de PR par statut</h2>
          <BarChart width={300} height={300} data={barData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis allowDecimals={false} />
            <Tooltip />
            <Bar dataKey="value" fill="#2196F3" />
          </BarChart>
        </div>

        <div className="bg-white p-4 rounded-lg shadow">
          <h2 className="text-lg font-semibold mb-4">Scores des PR</h2>
          <LineChart width={300} height={300} data={lineData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Line type="monotone" dataKey="score" stroke="#FF5722" />
          </LineChart>
        </div>
      </div>

      {/* Tableau filtré */}
      {loading ? (
        <p className="text-white">Chargement des Pull Requests...</p>
      ) : error ? (
        <p className="text-red-500">❌ Erreur : {error}</p>
      ) : filteredPRs.length === 0 ? (
        <p className="text-white">🚫 Aucune Pull Request trouvée pour ce filtre.</p>
      ) : (
        <div className="overflow-x-auto bg-white rounded-lg shadow">
          <table className="min-w-full text-sm text-left text-gray-700">
            
            <thead>
              <tr>
                <th className="px-4 py-2">ID</th>
                <th className="px-4 py-2">Repo</th>
                <th className="px-4 py-2">Titre</th>
                <th className="px-4 py-2">Auteur</th>
                <th className="px-4 py-2">Date</th>
                <th className="px-4 py-2">Score</th>
                <th className="px-4 py-2">Statut</th>
                <th className="px-4 py-2">Actions</th>
              </tr>
            </thead>
            <tbody>
              {paginatedPRs.map((pr) => (
                <React.Fragment key={pr.id}>
                  <tr className="border-b">
                    <td className="px-4 py-2">{pr.id}</td>
                    <td className="px-4 py-2">{pr.repo}</td>
                    <td className="px-4 py-2">{pr.title}</td>
                    <td className="px-4 py-2">{pr.auteur}</td>
                    <td className="px-4 py-2">{pr.date}</td>
                    <td className="px-4 py-2">{pr.score}</td>
                    <td className="px-4 py-2">{pr.statut}</td>
                    <td className="px-4 py-2">
                      <button
                        className="text-blue-500 hover:underline"
                        onClick={() => toggleComment(pr.id)}
                      >
                        {expandedRows[pr.id] ? "Masquer" : "Voir"}
                      </button>
                    </td>
                  </tr>
                  {expandedRows[pr.id] && (
                    <tr className="bg-gray-100">
                      <td colSpan={8} className="px-4 py-2 text-gray-700">
                        {pr.commentaires || "Aucun commentaire."}
                      </td>
                    </tr>
                  )}
                </React.Fragment>
              ))}
            </tbody>

              
          </table>

          {/* Pagination */}
          <div className="flex justify-between items-center mt-4 px-4 py-2 bg-gray-200 rounded-b-lg">
            <button
              onClick={handlePrevPage}
              disabled={currentPage === 1}
              className="flex items-center px-3 py-1 bg-blue-500 text-white rounded disabled:opacity-50"
            >
              <FaChevronLeft className="mr-1" /> Précédent
            </button>
            <span>
              Page {currentPage} / {totalPages}
            </span>
            <button
              onClick={handleNextPage}
              disabled={currentPage === totalPages}
              className="flex items-center px-3 py-1 bg-blue-500 text-white rounded disabled:opacity-50"
            >
              Suivant <FaChevronRight className="ml-1" />
            </button>
          </div>
        </div>
      )}
    </div>
  );
}

// Composant StatCard
function StatCard({ title, value, color, onClick, active, disabled }) {
  return (
    <div
      onClick={disabled ? undefined : onClick}
      className={`p-4 rounded-lg shadow cursor-pointer ${color} ${
        active ? "ring-2 ring-offset-2 ring-blue-400" : ""
      } ${disabled ? "opacity-70 cursor-default" : ""}`}
    >
      <h3 className="text-sm font-medium text-white">{title}</h3>
      <p className="text-2xl font-bold text-white">{value}</p>
    </div>
  );
}

