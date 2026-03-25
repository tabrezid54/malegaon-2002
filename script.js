const bucket = "https://voter-list-2002.s3.amazonaws.com/malegaon/";

let voters = [];

async function loadData() {
  const fileList = await fetch(bucket + "files.json").then(r => r.json());

  for (const f of fileList) {
    const res = await fetch(bucket + f);
    const json = await res.json();
    voters = voters.concat(json);
  }

  console.log("Loaded", voters.length, "records");
}
loadData();

