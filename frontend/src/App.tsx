import {FormEvent,useEffect,useState} from 'react';
type Player={id:number;name:string;city:string;level:number}; type Match={id:number;player_one_id:number;player_two_id:number;scheduled_at:string;venue:string;score:string|null};
const API=import.meta.env.VITE_API_URL ?? 'http://localhost:8000';
export function App(){
 const [players,setPlayers]=useState<Player[]>([]),[matches,setMatches]=useState<Match[]>([]),[name,setName]=useState('');
 const load=()=>Promise.all([fetch(`${API}/players`).then(r=>r.json()).then(setPlayers),fetch(`${API}/matches`).then(r=>r.json()).then(setMatches)]);
 useEffect(()=>{load()},[]);
 async function addPlayer(e:FormEvent){e.preventDefault();await fetch(`${API}/players`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name,city:'Bolzano',level:3})});setName('');load()}
 const pname=(id:number)=>players.find(p=>p.id===id)?.name??`#${id}`;
 return <main><header><span>MP</span><div><h1>MatchPoint</h1><p>Find your next match. Track every point.</p></div></header><section className="stats"><article><b>{players.length}</b><small>Players</small></article><article><b>{matches.length}</b><small>Matches</small></article><article><b>{matches.filter(m=>m.score).length}</b><small>Completed</small></article></section><div className="grid"><section className="card"><h2>Players</h2><form onSubmit={addPlayer}><input aria-label="Player name" value={name} onChange={e=>setName(e.target.value)} placeholder="Player name" minLength={2} required/><button>Add player</button></form>{players.map(p=><div className="row" key={p.id}><strong>{p.name}</strong><span>{p.city} · Level {p.level}</span></div>)}</section><section className="card"><h2>Upcoming & recent</h2>{matches.length===0?<p className="empty">No matches yet. Use the API docs to schedule the first one.</p>:matches.map(m=><div className="match" key={m.id}><strong>{pname(m.player_one_id)} vs {pname(m.player_two_id)}</strong><span>{m.score??new Date(m.scheduled_at).toLocaleString()} · {m.venue}</span></div>)}</section></div></main>
}


