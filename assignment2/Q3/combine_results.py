import json
import os

def combine_results(config_file="config.json", metrics_dir="results", output_file="combined_results.json"):
    # Load the configuration file
    with open(config_file, "r") as f:
        config_data = json.load(f)
    
    scenarios = config_data.get("scenarios", [])
    results = []

    # For each scenario, load the corresponding metrics log file
    for i, scenario in enumerate(scenarios):
        metrics_file = os.path.join(metrics_dir, f"metrics_{i}.log")
        try:
            with open(metrics_file, "r") as f:
                # Read the file content as a string.
                content = f.read()
                # Split the content into lines and remove the first line.
                lines = content.splitlines()
                # Check if the first line contains "Computed Metrics" and remove it.
                if lines and "Computed Metrics" in lines[0]:
                    json_str = "\n".join(lines[1:])
                else:
                    json_str = content
                # Load the remaining JSON string.
                metrics_data = json.loads(json_str)
        except Exception as e:
            print(f"Warning: could not load {metrics_file}: {e}")
            metrics_data = {}

        results.append({
            "scenario": i,
            "config": scenario,
            "metrics": metrics_data
        })
    
    # Create a combined JSON structure
    combined = {
        "configuration": config_data,
        "results": results
    }
    
    # Save the combined data into a JSON file
    with open(output_file, "w") as f:
        json.dump(combined, f, indent=4)
    print(f"Combined results written to {output_file}")

if __name__ == '__main__':
    combine_results()
