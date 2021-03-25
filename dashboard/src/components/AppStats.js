import React, { useEffect, useState } from 'react'
import '../App.css';

export default function AppStats() {
    const [isLoaded, setIsLoaded] = useState(false);
    const [stats, setStats] = useState({});
    const [error, setError] = useState(null)

	const getStats = () => {
	
        fetch(`http://taylor-lab6.eastus.cloudapp.azure.com:8100/stats`)
            .then(res => res.json())
            .then((result)=>{
				console.log("Received Stats")
                setStats(result);
                setIsLoaded(true);
            },(error) =>{
                setError(error)
                setIsLoaded(true);
            })
    }
    useEffect(() => {
		const interval = setInterval(() => getStats(), 2000); // Update every 2 seconds
		return() => clearInterval(interval);
    }, [getStats]);

    if (error){
        return (<div className={"error"}>Error found when fetching from API</div>)
    } else if (isLoaded === false){
        return(<div>Loading...</div>)
    } else if (isLoaded === true){
        return(
            <div>
                <h1>Latest Stats</h1>
                <table className={"StatsTable"}>
					<tbody>
						<tr>
							<th>Views</th>
							<th>Likes</th>
						</tr>
						<tr>
							<td># Views: {stats['views']}</td>
							<td># Likes: {stats['likes']}</td>
						</tr>
						<tr>
							<td colspan="2"># Comments: {stats['num_comments']}</td>
						</tr>
						{/* <tr>
							<td colspan="2">Max BR Diastolic: {stats['max_bp_dia_reading']}</td>
						</tr>
						<tr>
							<td colspan="2">Max HR: {stats['max_bp_sys_reading']}</td>
						</tr> */}
					</tbody>
                </table>
                <h3>Last Updated: {stats['timestamp']}</h3>

            </div>
        )
    }
}
