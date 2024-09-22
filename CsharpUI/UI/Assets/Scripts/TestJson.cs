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
    public Text textOrder1;
    public Text textOrder2;
    //public Text textOrder3;


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
                    ""weapon_url"": ""sanbaoju"",
                    ""price_list"": [
                        50,
                        60,
                        70
                    ]
                }
            ]
        }";

        // 解析JSON字符串
        OrdersContainer container = JsonUtility.FromJson<OrdersContainer>(jsonString);


        // 清空之前的文本内容
        textOrder1.text = "";
        textOrder2.text = "";

        // 遍历订单数据并更新UI控件
        if (container.orders.Length >= 1)
        {
            UpdateUITexts(container.orders[0], textOrder1);
        }
        if (container.orders.Length >= 2)
        {
            UpdateUITexts(container.orders[1], textOrder2);
        }
        // foreach (var order in container.orders)
        // {
        //     Debug.Log($"Order Name: {order.weapon_url}, Prices: [{order.price_list[0]}, {order.price_list[1]}, {order.price_list[2]}]");
        //     string text = $"Order Name: {order.weapon_url}, Prices: [{order.price_list[0]}, {order.price_list[1]}, {order.price_list[2]}]";
        //     printText.text = text;
        // }
    }
    private void UpdateUITexts(Order order,Text text)
    {
         if (order != null)
        {
            string orderInfo = $"Weapon URL: {order.weapon_url}\n";
            string priceListText = "Prices: [";
            for (int i = 0; i < order.price_list.Length; i++)
            {
                priceListText += $"{order.price_list[i]}";
                if (i < order.price_list.Length - 1)
                {
                    priceListText += ", ";
                }
            }
            priceListText += "]";

            text.text = orderInfo + priceListText;
        }
    }
}