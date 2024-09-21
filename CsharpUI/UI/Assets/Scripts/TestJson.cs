using UnityEngine;
using UnityEngine.UI;


[System.Serializable]
public class Order
{
    public string weapon_url;
    public int[] price_list;
}

[System.Serializable]
public class OrdersContainer
{
    public Order[] orders;
}

public class TestJson : MonoBehaviour
{
    public Button button;

    private void Start()
    {
        button.GetComponent<Button>().onClick.AddListener(Run);

    }
    public void Run()
    {
        string jsonString = @"
        {
            ""orders"": [
                {
                    ""weapon_url"": ""magistar"",
                    ""price_list"": [
                        500,
                        550,
                        550
                    ]
                },
                {
                    ""weapon_url"": ""magistar"",
                    ""price_list"": [
                        500,
                        550,
                        550
                    ]
                }
            ]
        }";

        // 解析JSON字符串
        OrdersContainer container = JsonUtility.FromJson<OrdersContainer>(jsonString);

        foreach (var order in container.orders)
        {
            Debug.Log($"Order Name: {order.weapon_url}, Prices: [{order.price_list[0]}, {order.price_list[1]}, {order.price_list[2]}]");
        }
    }
}