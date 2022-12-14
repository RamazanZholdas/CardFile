exports.handler = async (event, context) => {
    var response  = event.response;
    var headers  = response.headers;

    try {
        response = {
            'statusCode' : 200,
            'headers' : {
                'Access-Control-Allow-Headers':'*',
                'Access-Control-Allow-Origin':'*',
                'Access-Control-Allow-Methods':'*',
                'Accept':'*/*',
                'Content-Type':'application/json'
            },            
            'body': JSON.stringify({
                message:'Hello world'
            })
        }
    } catch (err) {
        console.log(err);
        return err;
    }
    return response
};