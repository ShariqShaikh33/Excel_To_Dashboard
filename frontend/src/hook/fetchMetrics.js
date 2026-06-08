import { useState } from "react";

export async function fetchMetrics(url) {
    try {
    const response = await fetch(url);
    console.log(response.status);
    if (!response.ok ) {
        throw new Error(`Failed to communicate with backend. Status: ${response.status}`);
    }
    
    const section = await response.json();
    console.log("Section",section)
    return section;
    } catch (err) {
    console.error("Fetch error:", err);
    }
}
